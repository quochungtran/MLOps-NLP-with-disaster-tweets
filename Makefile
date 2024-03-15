.PHONY:   build_app_image register_app_image app_local_up app_helm_up mlflow_up

# mlflow
mlflow_up:
	docker compose -f deployment/mlflow/docker-compose.yaml up -d

# deploy app in local
app_local_up:
	docker compose -f deployment/model_predictor/docker-compose.yaml up -d

# build image classifier app
build_app_image:
	docker build -f deployment/model_predictor/Dockerfile -t quochungtran/classify_disaster_text:0.0.1 .

register_app_image:
	docker push quochungtran/classify_disaster_text:0.0.1