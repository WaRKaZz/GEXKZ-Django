from django.shortcuts import render
# Create your views here.

games = [
	{
		'gamename': 'Zelda: Breath of the wild',
		'console': 'NS',
		'genre': 'Action',
		'image': 'gameexch/game-covers/zelda-botw-cover.jpg',
		'content': 'A lot of the game’s charm revolves around the fact that it rewards experimentation, so you are positively encouraged to go off script and explore out of the way areas of the map. The main story arc can be completed in a non-linear fashion, so you can choose how and when you complete each task rather than being forced into a restricted course of action. The game’s prize-winning graphics, physics engine and high-quality voice acting saw it being named Game of the Year and it has been touted as one of the greatest video games of all time as well as being – understandably – the best-selling Zelda game ever.',
		'likes': '3323',
	},
	{
		'gamename': 'The Elder Scrolls 5: Skyrim',
		'console': 'PS4',
		'genre': 'RPG',
		'image': 'static/gameexch/game-covers/tes-skyrim-cover.jpg',
		'content': 'A lot of the game’s charm revolves around the fact that it rewards experimentation, so you are positively encouraged to go off script and explore out of the way areas of the map. The main story arc can be completed in a non-linear fashion, so you can choose how and when you complete each task rather than being forced into a restricted course of action. The game’s prize-winning graphics, physics engine and high-quality voice acting saw it being named Game of the Year and it has been touted as one of the greatest video games of all time as well as being – understandably – the best-selling Zelda game ever.',
		'likes': '322',
	},
	{
		'gamename': 'The Elder Scrolls 5: Skyrim aasdasdds asdasd asdasd of the great',
		'console': 'NS',
		'genre': 'RPG',
		'image': 'static/gameexch/game-covers/tes-skyrim-cover.jpg',
		'content': 'A lot of the game’s charm revolves around the fact that it rewards experimentation, so you are positively encouraged to go off script and explore out of the way areas of the map. The main story arc can be completed in a non-linear fashion, so you can choose how and when you complete each task rather than being forced into a restricted course of action. The game’s prize-winning graphics, physics engine and high-quality voice acting saw it being named Game of the Year and it has been touted as one of the greatest video games of all time as well as being – understandably – the best-selling Zelda game ever.',
		'likes': '322',
	},
]

def home(request):
	context = {
		'games': games
	}
	return render(request, 'gameexch/home.html', context)

def about(request):
	return render(request, 'gameexch/about.html', {'title':'About'})
