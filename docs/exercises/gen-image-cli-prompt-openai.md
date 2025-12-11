# Prompt to create CLI application for OpenAI image generation

Create a simple and standalone CLI application for generating an image using the The OpenAI dall-e-3 image model (https://platform.openai.com/docs/guides/image-generation?image-generation-model=dall-e-3).
The OpenAI API key (OPENAI_API_KEY) is in the .env file (located in the root folder of the project).
Place the script under the gen-image folder and create a brief and concise README.md with usage instructions and examples.

## Technical requirements
- Implement the application using [LANGUAGE], and [ADDITIONAL_FRAMEWORKS_OR_LIBRARIES]
- Use best practices for CLI applications in the selected language
- Use minimal dependencies and make the application as standalone as possible
- Use the standard OpenAI API SDK if available for the selected language, otherwise use the the simplest client library possible

## Functional requirements
- Support specifying the prompt as an argument
- Support for apspect ratio (enum) parameter: auto (default), square (1024x1024) - portrait (1024x1792) - landscape (1792x1024)
- Support for quality parameter: - standard (default) - hd
- Support parameter for output file path
- Add a helper script to launch the CLI application (i.e. `gen-image.sh`)

## Example usage
```bash
cd gen-image
./gen-image.sh --prompt "A cute robot" [options]
```
