from flask import Flask, render_template, request, send_file
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)

def make_qr(link):
    """Generate a QR code image from a link."""
    qr_image = qrcode.make(link)  # Generate the QR code image
    return qr_image

def convert_qr_to_bytes(image):
    """Convert the QR code image to a BytesIO stream."""
    img_stream = BytesIO()  # Create a BytesIO stream to hold the image
    image.save(img_stream, 'PNG')  # Save the image to the BytesIO stream in PNG format
    img_stream.seek(0)  # Rewind the stream to the beginning
    return img_stream  # Return the BytesIO stream

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_img_data = None  # Initialize QR code image data to None

    if request.method == 'POST':
        link = request.form.get('link')  # Get the link from the form data
        download = 'download' in request.form  # Check if the download button was clicked

        if link:  # Validate the link
            qr_image = make_qr(link)  # Generate the QR code image
            img_stream = convert_qr_to_bytes(qr_image)  # Convert the image to a BytesIO stream

            if download:  # If download was requested
                img_stream.seek(0)  # Rewind the stream to the beginning
                return send_file(img_stream, mimetype='image/png', as_attachment=True, download_name='qr_code.png')  # Serve the image as a downloadable PNG file

            # Convert the image to a base64 string for inline display
            img_data = base64.b64encode(img_stream.getvalue()).decode('utf-8')
            qr_img_data = f"data:image/png;base64,{img_data}"

    # Render the template with qr_img_data being None or having the base64 data
    return render_template('qr.html', qr_img_data=qr_img_data)

if __name__ == '__main__':
    app.run(debug=True)
