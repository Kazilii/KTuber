from pytube import YouTube
import os
from shutil import copyfile
import sys

vab = 0

def settings():
	ls = []

	for f in os.listdir('./'):
		ls.append(f)

	vari = 'Y'

	if len(ls) > 3:
		vari = input('KTuber has detected that it is not being run in it\'s own folder, it is recommended to have a folder specifically for PyTuber. Do you wish to continue? (Y/n) ')

	if vari.lower() == 'n'.lower():
		print('Shutting down KTuber, please move the executable file into it\'s own folder and run again.')
		sys.exit("User opted shutdown.")

	vab = input('Would you like to download a video file, audio file, or both?(video|audio|both) ')

	if vab.lower() == 'audio':
		vab = 0
		download(vab)
		return

	if vab.lower() == 'video':
		vab = 1
		download(vab)
		return

	if vab.lower() == 'both':
		vab = 2
		download(vab)
		return

	else:
		input('Invalid selection, press enter to restart.')
		settings()

def download(vab=0):

	try:
		yt = YouTube(input('Input youtube link: '))
		yt.streams.first().download('download')
		if vab >= 1:
			copyfile('download/' + str(os.listdir('download')[0]), 'media/' + str(os.listdir('download')[0]))
	except:
		input('Invalid youtube link, press enter to try again.')
		download()

	if vab == 1:
		cleanup()
		return

	audioname = ""

	for f in os.listdir('download'):
		audioname = f.replace('.mp4', '.mp3')
		os.rename('download/{0}'.format(f), 'download/video.mp4')

	import moviepy.editor as mp

	clip = mp.VideoFileClip('download/video.mp4')
	clip.audio.write_audiofile('media/{0}'.format(audioname))
	clip.close()
	cleanup()

def cleanup():
	for f in os.listdir('download'):
		os.remove('download/{0}'.format(f))

def checkfolder():
	if not os.path.exists('download'):
		os.makedirs('download')
	if not os.path.exists('media'):
		os.makedirs('media')

checkfolder()
cleanup()
settings()
