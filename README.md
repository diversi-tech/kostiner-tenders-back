## Getting Started

A basic pattern of Python's backend



### Installation

To work with this project, a virtual environment is required

1. Clone the repo
   ```sh
   git clone https://github.com/diversi-tech/kostiner-tenders-back.git
   ```
2. Creating a new virtual environment:
   ```sh
   python -m venv .venv
   ```
3. Activating the virtual environment:
   ```sh
   .venv\Scripts\activate
   ```
4. Install dependencies:
   Make sure you have a requirements.txt file in the project, which contains all project dependencies.
   Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```
5. run:
   ```shell
   python -m flask run
   ```

### Dockerfile
1. Build the Docker image:
   ```shell
   docker build -t kostiner .
   ```
2. Run the Docker container:
   ```shell
   docker run -p 5000:5000 --env-file .env kostiner
   ```
<!-- CONTRIBUTING -->
## Contributing

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some Feature'`)
4. Push to the Branch (`git push origin feature/Feature`)
5. Open a Pull Request


