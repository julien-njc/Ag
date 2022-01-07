import pdf2image
from pdf2image import convert_from_path
import os
import time


start_time = time.time()
##################################################
#####
##### Flat
#####
main_in = "/data/hydro/users/Hossein/NASA/06_snapshot_flat/"
main_out ="/data/hydro/users/Hossein/NASA/06_snapshot_flat_PNG/"

os.makedirs(main_out, exist_ok=True)


PDF_fiels = [x for x in os.listdir(main_in) if x.endswith(".pdf")]
for a_pdf_file in PDF_fiels:
    if "corrected" in a_pdf_file or "TOA" in a_pdf_file:
        image = convert_from_path(main_in + a_pdf_file, dpi=50, poppler_path="./.local/lib/python3.7/site-packages")
        image[0].save(f'/{main_out}{a_pdf_file[0:-4]}.png')
    else:
        image = convert_from_path(main_in + a_pdf_file, dpi=100, poppler_path=None)
        image[0].save(f'/{main_out}{a_pdf_file[0:-4]}.png')


end_time = time.time()
print ("it took {:.0f} minutes to run this code.".format((end_time - start_time)/60))
