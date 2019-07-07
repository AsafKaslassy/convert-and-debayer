import os
import subprocess as sp


def replace_file(src_file, replacements, dst_file):

    """
    :param src_file: str - template file loaction
    :param replacements: dictionary contains strings and their suitable replacements
    :param dst_file: str - runner file loaction
    :Description: This function writes a new text file with changes based on template file and replacements strings.
    """

    src_file = open(src_file, 'r')

    dst_file = open(dst_file, 'w')
    for line in src_file:
        for src, target in replacements.iteritems():
            line = line.replace(src, target)
        dst_file.write(line)
    src_file.close()
    dst_file.close()


def convert_raw_to_tiff(input_dir, irfan_view_path):

    """
    :param config: Configuration dictionary
    :param log: replayLogger object instance
    :Description: This function converting RAW images to Tiff
    """

    raw_images_path = os.path.join(input_dir, r'raw')
    tiff_images_path = os.path.join(input_dir, r'tiff')
    if not os.path.exists(tiff_images_path):
        os.mkdir(tiff_images_path)
    cmd = os.path.join(irfan_view_path, r'i_view32.exe ') + os.path.join(raw_images_path, r'*.raw /convert=') + \
        os.path.join(tiff_images_path, r'*.tif')
    sp.call(cmd)


def debayer_images(input_dir, pip_path, static_path):

    """
    :param config: Configuration dictionary
    :param log: replayLogger object instance
    :Description: This function debayering images
    """

    raw_images_path = os.path.join(input_dir, r'tiff')
    workdir_path = os.path.join(input_dir, r'workdir')
    if not os.path.exists(workdir_path):
        os.mkdir(workdir_path)
    output_path = os.path.join(input_dir, r'debayer')
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    lut_path = os.path.join(static_path, r'NATUERAL_LUT.tif')
    bayer_template_file = os.path.join(static_path, r'bayer_template_file.xml')
    raw_images = os.listdir(raw_images_path)

    counter = 1
    for image in raw_images:
        replace_file(bayer_template_file, {'{Pi_path}': pi_path,
                                           '{input_image}': os.path.join(raw_images_path, image),
                                           '{output_image}': os.path.join(output_path, r'%04d.jpg' % counter),
                                           '{LUT_path}': lut_path},
                     os.path.join(workdir_path, 'tempBayer.xml'))
        cmd = os.path.join(pip_path, r'Pi.exe ') + os.path.join(workdir_path, 'tempBayer.xml')
        sp.call(cmd)
        counter += 1


def run():

    work_dir_path = r'D:\Mavericks'
    static_path = r'C:\Apps\UndistortTool\staticFiles'
    irfan_view_path = r'C:\Program Files (x86)\IrfanView'
    pip_path = r'C:\Apps\PI'
    lens_list = os.walk(work_dir_path).next()[1]
    for lens in lens_list:
        lens_modes_list = os.walk(os.path.join(work_dir_path, lens)).next()[1]
        for mode in lens_modes_list:

            convert_raw_to_tiff(os.path.join(work_dir_path, lens, mode), irfan_view_path)
            debayer_images(os.path.join(work_dir_path, lens, mode), pip_path, static_path)


if __name__ == '__main__':
    run()