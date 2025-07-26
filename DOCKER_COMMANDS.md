# Docker Build and Test Commands

## Build the Docker image

```bash
docker build --platform linux/amd64 -t adobe-hackathon:round1a .
```

## Test the Docker image (when you have PDF files in input/)

```bash
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none adobe-hackathon:round1a
```

## Alternative test on Windows PowerShell

```powershell
docker run --rm -v ${PWD}/input:/app/input -v ${PWD}/output:/app/output --network none adobe-hackathon:round1a
```

## Check results

After running, check the `output/` directory for JSON files corresponding to each PDF in `input/`.

## Sample Expected Output Format

```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
```
