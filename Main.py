import os
from PIL import Image
import pillow_heif
import piexif

def convert_heic_to_png(source_folder, destination_folder):
    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for filename in os.listdir(source_folder):
        if filename.lower().endswith('.heic'):
            heic_path = os.path.join(source_folder, filename)
            png_filename = os.path.splitext(filename)[0] + '.png'
            png_path = os.path.join(destination_folder, png_filename)

            # Open HEIC image using pillow_heif
            heif_file = pillow_heif.open_heif(heic_path)

            # Extract EXIF data
            exif_data = heif_file.info.get('exif', None)
            exif_dict = piexif.load(exif_data) if exif_data else None

            # Convert HEIC file to a PIL image
            image = Image.frombytes(
                heif_file.mode,
                heif_file.size,
                heif_file.data,
                "raw",
                heif_file.mode,
                heif_file.stride,
            )

            # Save the image in PNG format with EXIF data
            if exif_dict:
                exif_bytes = piexif.dump(exif_dict)
                image.save(png_path, format="PNG", exif=exif_bytes)
            else:
                image.save(png_path, format="PNG")

            print(f"Converted {filename} to {png_filename} with metadata")

if __name__ == "__main__":
    source_folder = 'Path/to/your/HEIC/files'
    destination_folder = 'Path/to/your/PNG/files/to/save'
    convert_heic_to_png(source_folder, destination_folder)
