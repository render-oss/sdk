package callbackapi

//go:generate go run github.com/oapi-codegen/oapi-codegen/v2/cmd/oapi-codegen@v2.4.1 -generate types,client,chi-server,strict-server -package callbackapi -o api_gen.go $RENDER_API_PATH/pkg/durableworkflow/callbackapi/openapi.yaml
