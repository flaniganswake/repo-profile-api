FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /repo_profile_service
WORKDIR /repo_profile_service
ADD . /repo_profile_service/
RUN pip install -r requirements.txt
COPY . /repo_profile_service
EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["run.py"]
