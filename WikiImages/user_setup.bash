echo "Setup"

#upgrade everything
echo "Updating..."
sudo apt-get update -y
sudo apt-get dist-upgrade -y
echo "Installing Python..."
sudo apt-get install python2.7-dev -y
echo "Installing libxml..."
sudo apt-get install libxml12-dev -y
sudo apt-get install libxslt1-dev -y
echo "Installing pip..."
sudo apt-get install python-pip -y
echo "Installing git..."
sudo apt-get install git -y
echo "Installing bs4..."
sudo apt-get install python-bs4 -y
echo "Installing selenium..."
sudo pip install selenium
