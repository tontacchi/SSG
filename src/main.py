#---[ Global Imports ]----------------------------------------------------------
from textnode import TextNode, TextType

#---[ Global Imports ]----------------------------------------------------------


#---[ Main Function ]-----------------------------------------------------------
def main():
    node = TextNode("This is some anchor text", TextType.LINK_TEXT, "https://www.boot.dev")
    print(node)

    normal_node_1 = TextNode("This is normal text", TextType.NORMAL_TEXT)
    normal_node_2 = TextNode("This is normal text", TextType.NORMAL_TEXT)

    print(normal_node_1)
    print(normal_node_2)

    print(normal_node_1 == normal_node_2)
    print(node == normal_node_1)
    print(node == normal_node_2)

    return

#---[ Main Function ]-----------------------------------------------------------


#---[ Entry ]-------------------------------------------------------------------
if __name__ == "__main__":
    main()

#---[ Entry ]-------------------------------------------------------------------
