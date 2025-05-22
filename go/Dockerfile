FROM golang:1.23-alpine

WORKDIR /app

COPY . .

RUN go build -o main ./example/main.go

CMD ["./main"]
