# MC Written Book Generator

This is a Python tool that allows you to generate written books in Minecraft based on a text file. If the text is too long, it will automatically split the written book into volumes. The tool supports various options for customization, such as specifying the encoding format,written book title, and author.

## Usage

To use the tool, run the following bash command:

```bash
python main.py <text_file_path> [-e <encoding_format>] [-t <title>] [-a <author>]
```

- `<text_file_path>`: The path to the text file containing the content for the written book.
- `<encoding_format>` (optional): The encoding format of the text file. If not specified, the default is utf-8.
- `<title>` (optional): The title of the written book. You can use the placeholder {volume} in the title, and it will be automatically replaced with the volume number during the generation process.
- `<author>` (optional): The author of the written book.

## Troubleshooting

If you encounter a “ValueError: Width data without character "..." ” during the generation process, you can add the width data for the character to the extended_width.json file.

## Customization

If you prefer, you can also import this Python package and utilize the provided interfaces to customize the generation rules. The package provides the following classes and methods:

- `create_book_collection`: A method used to generate a collection of written books.
- `Book`: A class used to generate individual written books.
- `Page`: A class used to generate book pages.

Feel free to explore the package and customize the generation process according to your needs.
