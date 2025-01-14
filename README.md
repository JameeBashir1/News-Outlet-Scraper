# To Run Directly in Github CodeSpace

## Step 1 Run Below Commands to Setup in Github CodeSpace:
1. sudo apt update
2. sudo apt upgrade -y
3. wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
4. sudo apt-get install -y ./google-chrome-stable_current_amd64.deb
5. rm -rf google-chrome-stable_current_amd64.deb
6. pip3 install -r requirements.txt
7. python NewsOutletScrapper.py
## Step 2 Update the UserName and Password in Yaml File
`userName: YOUR_USERNAME'
`accessKey: YOUR_ACCESS_KEY`
## Step 3 To Run the Tests on BrowserStack using the Pytest SDK
`browserstack-sdk python NewsOutletScrapper.py`
# WorkFlows
### The project is seamlessly integrated with GitHub Actions, enabling automated workflows that streamline processes such as testing, deployment, and more. These workflows are triggered by events like code pushes, pull requests, or manual invocations. This integration ensures early detection of issues, maintains consistent quality standards, and accelerates the development cycle with reliable, automated processes.
# Tested on BrowserStack
[View ScreenShot](https://drive.google.com/file/d/15xxNY2fZEDKVVqRf3h-8ylvBVygdcsAw/view?usp=sharing)

# To Run Locally 
## Step 1 Clone the Repository
`https://github.com/JameeBashir1/News-Outlet-Scraper`
cd News-Outlet-Scraper
## Step 2 Install Requirements
`pip install -r requirements.txt`
## Step 3 Update the UserName and Password in Yaml File
`userName: jameebashir_ncy6hC'
`accessKey: LmQ2BVMHePvSQVy5sxYi`
## Step 4 To test locally
`python NewsOutletScrapper.py`
or
`python3 NewsOutletScrapper.py`
## Step 5 To Run the Tests on BrowserStack using the Pytest SDK
`browserstack-sdk python NewsOutletScrapper.py`
