# 1. Build the Docker image:
# ./docker-run.sh build

# 2. Run all tests:
# ./docker-run.sh test

# 3. Run the demo:
# ./docker-run.sh demo

if [ -z "$1" ]; then
    echo "Usage: $0 [command]"
    echo ""
    echo "Available commands:"
    echo "  build    - Build Docker image"
    echo "  test     - Run all tests"
    echo "  demo     - Run short demo"
    echo ""
    exit 1
fi

case "$1" in
    "build")
        echo "Building Docker image..."
        docker-compose build
        ;;
    "test")
        echo "Running all tests..."
        docker-compose run --rm test
        ;;
    "demo")
        echo "Running demo..."
        docker-compose up app
        ;;
    *)
        echo "Unknown command: $1"
        echo "Use: build, test, or demo"
        exit 1
        ;;
esac