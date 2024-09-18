import streamlit as st
import imagehash
import os
import time
from Crypto.Cipher import DES
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from PIL import Image

with open('/home/jayk/Projects/TRIPLE_DES/mystyle.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

title1 = '<h1>[Triple DES]</h1>'
st.markdown(title1, unsafe_allow_html=True)

title2 = "<h2 >Image Encryption and Decryption</h2><br><br><br>"
st.markdown(title2, unsafe_allow_html=True)

footer = """<style>
.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
font-family: Blueberry Days;
}
</style>
<div class="footer">
<p>Developed with ❤ by <a style='display: block; text-align: center;'  target="_blank">Jay Kawa / Anas Khan / Brijesh Kori</a></p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)


def progressbar():
    my_bar = st.progress(0)

    for percent_complete in range(100):
        time.sleep(0)
        my_bar.progress(percent_complete + 1)


def spin_encrypt():
    with st.spinner('encrypting...'):
        time.sleep(2)
    st.success('ENCRYPTION SUCCESSFUL!!!')


def spin_decrypt():
    with st.spinner('decrypting...'):
        time.sleep(2)
    st.success('DECRYPTION SUCCESSFUL!!!')


def encryptor(path, name):
    pi = 100005
    salt_const = b"$ez*}-d3](%d%$#*!)$#%s45le$*fhucdivyanshu75456dgfdrrrrfgfs^"

    try:
        with open(path, 'rb') as imagefile:
            image = imagefile.read()

        while len(image) % 8 != 0:
            image += b" "
    except:
        st.text("Error loading the file, make sure file is in same directory, spelled correctly and non-corrupted")

    hash_of_original = SHA256.new(data=image)
    key_enc = st.text_input(label="Password", type="password", max_chars=24, placeholder="Enter Password",
                            help="Minimum 8 character long password Required", key="1")

    if key_enc:

        key_enc = PBKDF2(key_enc, salt_const, 48, count=pi)

        try:
            cipher1 = DES.new(key_enc[0:8], DES.MODE_CBC, key_enc[24:32])
            ciphertext1 = cipher1.encrypt(image)
            cipher2 = DES.new(key_enc[8:16], DES.MODE_CBC, key_enc[32:40])
            ciphertext2 = cipher2.decrypt(ciphertext1)
            cipher3 = DES.new(key_enc[16:24], DES.MODE_CBC, key_enc[40:48])
            ciphertext3 = cipher3.encrypt(ciphertext2)
            spin_encrypt()
        except:
            st.text(
                'Encryption failed...Possible causes:Library not installed properly/low device memory/Incorrect padding or conversions')

        ciphertext3 += hash_of_original.digest()

        dpath = "encrypted_" + name
        saved = "/home/jayk/Downloads/" + dpath
        with open(saved, 'wb') as image_file:
            image_file.write(ciphertext3)
        st.info("			Encrypted Image Saved successfully as filename " + dpath, icon="ℹ️")
        with open(saved, "rb") as image_file:
            btn = st.download_button(
                label="Download image",
                data=image_file,
                file_name="Encrypted.png",
                mime="image/png"
            )


def upload_encrypt():

    uploaded_files = st.file_uploader("Image Upload", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()

        if uploaded_file.name is not None:
            with open(os.path.join("/home/jayk/Downloads/", uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())
            path = os.path.join("/home/jayk/Downloads/", uploaded_file.name)
            name = uploaded_file.name
            progressbar()
            image = Image.open(path)
            st.image(image, caption='')
            encryptor(path, name)


def decryptor(encrypted_image_path, name):
    pi = 100005
    salt_const = b"$ez*}-d3](%d%$#*!)$#%s45le$*fhucdivyanshu75456dgfdrrrrfgfs^"

    try:
        with open(encrypted_image_path, 'rb') as encrypted_file:
            encrypted_data_with_hash = encrypted_file.read()

    except:
        st.warning("Unable to read source cipher data. ")

    key_dec = st.text_input(label="Enter Password", type="password", max_chars=24,
                            help="Minimum 8 character long password Required", key="2")
    if key_dec:
        extracted_hash = encrypted_data_with_hash[-32:]
        encrypted_data = encrypted_data_with_hash[:-32]

        key_dec = PBKDF2(key_dec, salt_const, 48, count=pi)

        try:

            cipher1 = DES.new(key_dec[16:24], DES.MODE_CBC, key_dec[40:48])
            plaintext1 = cipher1.decrypt(encrypted_data)
            cipher2 = DES.new(key_dec[8:16], DES.MODE_CBC, key_dec[32:40])
            plaintext2 = cipher2.encrypt(plaintext1)
            cipher3 = DES.new(key_dec[0:8], DES.MODE_CBC, key_dec[24:32])
            plaintext3 = cipher3.decrypt(plaintext2)

        except:
            st.warning(
                "			Decryption failed...Possible causes:Library not installed properly/low device memory/Incorrect padding or conversions")

        hash_of_decrypted = SHA256.new(data=plaintext3)
        if hash_of_decrypted.digest() == extracted_hash:
            st.success("Password Correct !!!")
            spin_decrypt()
            epath = name
            if epath[:10] == "encrypted_":
                epath = epath[10:]
            epath = "decrypted_" + epath
            saved = "/home/jayk/Downloads/" + epath
            with open(saved, 'wb') as image_file:
                image_file.write(plaintext3)
            st.info("			Decrypted Image Saved successfully as filename " + epath, icon="ℹ️")
            with open(saved, "rb") as image_file:
                btn = st.download_button(
                    label="Download image",
                    data=image_file,
                    file_name="Decrypted.png",
                    mime="image/png"
                )
        else:
            st.warning("Incorrect Password!!!")


def upload_decrypt():
    uploaded_files = st.file_uploader("Encrypted Image Upload", accept_multiple_files=True,
                                      key="3")
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()

        if uploaded_file.name is not None:
            with open(os.path.join("/home/jayk/Downloads/", uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())
            encrypted_image_path = os.path.join("/home/jayk/Downloads/", uploaded_file.name)
            name = uploaded_file.name
            progressbar()
            decryptor(encrypted_image_path, name)

def compare_images():
    
    uploaded_files = st.file_uploader("Original Image Upload", accept_multiple_files=True, key="4")
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()

        if uploaded_file.name is not None:
            with open(os.path.join("/home/jayk/Downloads/", uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())
            path = os.path.join("/home/jayk/Downloads/", uploaded_file.name)
            name = uploaded_file.name
            progressbar()

    uploaded_files1 = st.file_uploader("Decrypted Image Upload", accept_multiple_files=True, key="5")
    for uploaded_file in uploaded_files1:
        bytes_data = uploaded_file.read()

        if uploaded_file.name is not None:
            with open(os.path.join("/home/jayk/Downloads/", uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())
            path1 = os.path.join("/home/jayk/Downloads/", uploaded_file.name)
            name = uploaded_file.name
            progressbar()


            col1, col2 = st.columns(2)

            with col1:

                image = Image.open(path)
                st.image(image, caption='Original Image')

            with col2:

                image = Image.open(path1)
                st.image(image, caption='Decrypted Image')

            HDBatmanHash = imagehash.dhash(Image.open(path))
            st.info('Original Image Hash: ' + str(HDBatmanHash))

            SDBatmanHash = imagehash.dhash(Image.open(path1))
            st.info('Decrypted Image Hash: ' + str(SDBatmanHash))

            if(HDBatmanHash == SDBatmanHash):
                st.success("The pictures are same !")
            else:
                st.error("The pictures are different")



if __name__ == '__main__':
    tab1, tab2, tab3 = st.tabs(["🔐 Encryption", "🔓 Decryption", "Cᴏᴍᴘᴀʀᴇ Iᴍᴀɢᴇs"])

    with tab1:
        upload_encrypt()

    with tab2:
        upload_decrypt()
    
    with tab3:
        compare_images()

