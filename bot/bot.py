import discord
import time
import subprocess
from os import system

with open("token", "r") as f:
	TOKEN = f.read().rstrip()

client = discord.Client();

BLEEDING = False
try:
	from git import Repo
	repo = Repo('.')
	branch = repo.active_branch

	if(branch.name == "bleeding"):
		BLEEDING = True
		print("*** Bleeding edge ***")
except:
	print("Couldn't check branch, assuming master")
	#TODO: fallback

async def wtf(M):
	await client.add_reaction(M, "❓")

async def nope(M):
	await client.add_reaction(M, "🚫")

async def pull(M):
	proc = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
	(out, err) = proc.communicate()
	out = out.decode()
	if(out != "Already up-to-date\n"):
		await client.send_message(M.channel, "```\n"+out+"\n```")

async def make(M):
	await client.send_typing(M.channel)
	proc = subprocess.Popen(["./make.sh"], stdout=subprocess.PIPE)
	(out, err) = proc.communicate()
	out = out.decode()
	await client.send_message(M.channel, "```\n"+out+"\n```")

async def stratish(M, words):
	if(words[0]!=' '):
		await wtf(M)
		return

	await client.send_typing(M.channel)
	ut = time.strftime("%s")
	tmpfile = "tmp/img-"+str(ut)+".png"
	command = "writer/sbdraw '%s' '%s'" % (words, tmpfile)
	print("$", command)
	system("touch "+tmpfile)
	system(command)
	await client.send_file(M.channel, tmpfile, content="`"+words+"`")
	

###############################################################################


@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	#await client.change_presence(game=discord.Game(name='/stratish ...'))
	



@client.event
async def on_message(M):
	print("#"+M.channel.name,"\t<"+str(M.author)+">\t", M.content)
	
	if(BLEEDING):
		if(M.content.startswith('/bleeding')):
			await stratish(M, M.content[9:])
	else:
		if(M.content.startswith('/stratish')):
			await stratish(M, M.content[9:])
		if(M.content.startswith('/s') or M.content.startswith("/S")):
			await stratish(M, M.content[2:])
	
	if(M.content.startswith('/pull')):
		await pull(M)
	
	if(M.content.startswith('/make')):
		await make(M)
	
	if(M.content.startswith('/chnick')):
		if(M.author.id == "247841704386756619"):
			await client.change_nickname(M.server.me, M.content[7:])
		else:
			await client.send_message(M.channel, "no.")
	
	if(str(M.author) == "GitHub#0000"):
		await pull(M)
		

client.run(TOKEN);
