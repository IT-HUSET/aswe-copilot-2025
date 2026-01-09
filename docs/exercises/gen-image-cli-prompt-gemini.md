# Prompt to create CLI application for Gemini Nano Banana image generation

Create a simple and standalone CLI application for generating an image using the Gemini 2.5 Flash Image model, a.k.a. `gemini-2.5-flash-image` (https://ai.google.dev/gemini-api/docs/models#gemini-2.5-flash).
The Gemini API key (GEMINI_API_KEY) is in the .env file (located in the root folder of the project).
Place the script under the gen-image folder and create a brief and concise README.md with usage instructions and examples.

## Technical requirements
- Implement the application using [LANGUAGE], and [ADDITIONAL_FRAMEWORKS_OR_LIBRARIES]
- Use best practices for CLI applications in the selected language
- Use minimal dependencies and make the application as standalone as possible
- Use the standard Gemini API SDK if available for the selected language, otherwise use the the simplest client library possible

## Functional requirements
- Support specifying the prompt as an argument
- Support parameter for aspect_ratio - 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9 (default), 21:9
- Support parameter for image_size - 1K, 2K (default), 4K
- Support parameter for output file path
- Add a helper script to launch the CLI application (i.e. `gen-image.sh`)

## Example usage
```bash
cd gen-image
./gen-image.sh --prompt "A cute robot" [options]
```
