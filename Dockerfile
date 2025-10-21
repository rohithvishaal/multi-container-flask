FROM python:slim
WORKDIR /app
COPY . /app/
RUN pip install -r requirements.txt
EXPOSE 5000
CMD sh -c "python load_data.py && python app.py"