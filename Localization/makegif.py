import matplotlib.pyplot as plt
import os
import imageio

def generate_gif(gif_name, png_dir, dpi=90):
    # make png path if it doesn't exist already
	if not os.path.exists(png_dir):
		print('invalid path')
        #os.makedirs(png_dir)



    # save each .png for GIF
    # lower dpi gives a smaller, grainier GIF; higher dpi gives larger, clearer GIF
    

    #plt.savefig(png_dir+'frame_'+str(gif_indx)+'_.png',dpi=dpi)
    #plt.close('all') # comment this out if you're just updating the x,y data

    #if gif_indx==num_gifs-1:
        # sort the .png files based on index used above
	images,image_file_names = [],[]
	for file_name in os.listdir(png_dir):
		if file_name.endswith('.png'):
			image_file_names.append(file_name)       
	sorted_files = sorted(image_file_names, key=lambda y: int(y.split('_')[1]) )

    # define some GIF parameters

	frame_length = 0.2 # seconds between frames
	end_pause = 2 # seconds to stay on last frame
        
	for ii in range(0,len(sorted_files)):       
		file_path = os.path.join(png_dir, sorted_files[ii])
		if ii==len(sorted_files)-1:
			for jj in range(0,int(end_pause/frame_length)):
				images.append(imageio.imread(file_path))
		else:
			images.append(imageio.imread(file_path))
    # the duration is the time spent on each image (1/duration is frame rate)
	imageio.mimsave(gif_name, images,'GIF',duration=frame_length)
