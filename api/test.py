from api.index import app

if __name__ == '__main__':
    print("Starting test server...")
    print("Make sure NOTION_TOKEN and NOTION_DATABASE_ID are set in your environment")
    app.run(port=3000, debug=True) 