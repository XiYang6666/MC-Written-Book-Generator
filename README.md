# MC Written Book Generator

This is a Python tool that allows you to generate books in Minecraft based on a text file. If the text is too long, it will automatically split the book into volumes. The tool supports various options for customization, such as specifying the encoding format, book title, and author.

## Usage

To use the tool, run the following bash command:

```bash
python main.py <text_file_path> [-e <encoding_format>] [-t <title>] [-a <author>]
```

- &lt;text_file_path&gt;: The path to the text file containing the content for the book.
- &lt;encoding_format&gt; (optional): The encoding format of the text file. If not specified, the default is utf-8.
- &lt;title&gt; (optional): The title of the book. You can use the placeholder {volume} in the title, and it will be automatically replaced with the volume number during the generation process.
- &lt;author&gt; (optional): The author of the book.

## Troubleshooting

If you encounter a “ValueError: Width data without character "..." ” during the generation process, you can add the width data for the character to the extended_width.json file.

## Customization

If you prefer, you can also import this Python package and utilize the provided interfaces to customize the generation rules. The package provides the following classes and methods:

- `create_book_collection`: A method used to generate a collection of books.
- `Book`: A class used to generate individual books.
- `Page`: A class used to generate book pages.

Feel free to explore the package and customize the generation process according to your needs.

Please note that this tool does not support any legal or political content or any information related to Chinese officials.
