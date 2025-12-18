# For context on this stuff, see https://slab.render.com/posts/cpu-throttling-exploration-notes-93q2yr2p#hlkc9-the-workload
FROM amd64/ubuntu:22.04 AS cpu-burner-build
WORKDIR /app
# All of this to install cpu_burner at /app/tlpi-dist/timers/cpu_burner
# TODO multi-stage build this shit
RUN apt-get update \
  && apt-get install -yq --no-install-recommends \
    stress libselinux1-dev libacl1-dev libcap-dev make wget gcc
RUN wget --no-check-certificate https://man7.org/tlpi/code/download/tlpi-230522-dist.tar.gz
RUN tar xfz tlpi-230522-dist.tar.gz
RUN cd tlpi-dist && make

FROM golang:1.24-alpine AS go-sdk-build

WORKDIR /app

# Copy go.mod and go.sum first for better caching
COPY go.mod go.sum ./

# Download dependencies (this layer will be cached unless go.mod/go.sum change)
RUN go mod download

# Copy source code
COPY . .

RUN go build -o main ./example/task

FROM amd64/ubuntu:22.04

COPY --from=cpu-burner-build /app/tlpi-dist/timers/ /app/timers

# Install tools for debugging
RUN apt-get update \
  && apt-get install -yq --no-install-recommends \
    socat stress-ng fio

RUN groupadd -g 1000 render
RUN useradd -u 1000 -g render render

WORKDIR /app

COPY --from=go-sdk-build /app/main /app/main

CMD ["./main"]
