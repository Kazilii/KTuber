from pytube import YouTube
import os
from shutil import copyfile
import subprocess
import sys
import platform

if platform.system() == 'Windows':
	import win32com.client
	objShell = win32com.client.Dispatch('WScript.Shell')
	DOC = objShell.SpecialFolders('MyDocuments')
	DOWNLOAD = DOC + '/KTuber/download'
	MEDIA = DOC + '/KTuber/media'
else:
	DOWNLOAD = 'download'
	MEDIA = 'media'

vab = 0

def settings():
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
		yt = YouTube(input('Input youtube link: ').replace(" ", ""))
		yt.streams.first().download(DOWNLOAD)
		if vab >= 1:
			copyfile(DOWNLOAD + '/' + str(os.listdir(DOWNLOAD)[0]), MEDIA + '/' + str(os.listdir(DOWNLOAD)[0]))
	except:
		input('Invalid youtube link, press enter to try again.')
		download()

	if vab == 1:
		cleanup()
		return

	audioname = ""

	for f in os.listdir(DOWNLOAD):
		audioname = f.replace('.mp4', '.mp3')
		os.rename(DOWNLOAD + '/{0}'.format(f), DOWNLOAD + '/video.mp4')

	import moviepy.editor as mp

	clip = mp.VideoFileClip(DOWNLOAD + '/video.mp4')
	clip.audio.write_audiofile(MEDIA + '/{0}'.format(audioname))
	clip.close()
	if platform.system() == 'Windows':
		os.startfile(MEDIA)
	if platform.system() == 'Linux':
		subprocess.Popen(['xdg-open', MEDIA])

	cleanup()

def cleanup():

	for f in os.listdir(DOWNLOAD):
		os.remove(DOWNLOAD + '/{0}'.format(f))

def checkfolder():
	if not platform.system() == 'Windows':
		if not os.path.exists('download'):
			os.makedirs('download')
		if not os.path.exists('media'):
			os.makedirs('media')
	else:
		if not os.path.exists(DOC + '/KTuber'):
			os.makedirs(DOC + '/KTuber')
		if not os.path.exists(DOC + '/KTuber/download'):
			os.makedirs(DOC + '/KTuber/download')
		if not os.path.exists(DOC + '/KTuber/media'):
			os.makedirs(DOC + '/KTuber/media')

checkfolder()
cleanup()
settings()
