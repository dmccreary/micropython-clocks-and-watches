# Generating a Glossary of Terms

## Prompt

!!! prompt
    Prompt Name: Glossary for Clocks and Watches with MicroPython Book

    You are an expert at creating a glossary of terms for
    books for high-school students.  You create precise, concise, distinct
    definitions that are non-circular and do not include rules.

    Your terms are written for the 9th grade reading level.
    
    The focus of this glossary is to support a book and website about 
    how to create DIY Clocks and Watches with MicroPython using the
    Raspberry Pi Pico W.  The project covers how to write MicroPython
    that integrates a variety of small low-cost displays as well as
    use real-time clocks and web services to get time information.

    For each term, return a term label in a level 4 markdown header.
    Place a precise, concise, distinct, non-circular definition
    after the header in a separate paragraph.  Do not include the term
    in the definitions.

   Go to the project area and use the file MicroPython_Clock_Concepts.csv
   for a complete list of concepts that need definitions.

    If appropriate create an example of how that term might be
    used in the website.  Use **Example:** with no newline after it.

    Return the entire glossary of terms in a single Markdown file
    for all concepts in alphabetical order.