from benedict.service import create_app

app = create_app(env="Production")

if __name__ == "__main__":
	app.run()