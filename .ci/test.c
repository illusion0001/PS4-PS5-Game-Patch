#include <mxml.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define u8 uint8_t
#define u16 uint16_t
#define u32 uint32_t
#define u64 uint64_t
#define s8 int8_t
#define s16 int16_t
#define s32 int32_t
#define s64 int64_t
#define f32 float
#define f64 double

static const char* GetXMLAttr(mxml_node_t *node, const char *name)
{
    const char* AttrData = mxmlElementGetAttr(node, name);
    if (AttrData == NULL) AttrData = "";
    return AttrData;
}

static const char *xml_whitespace_cb(mxml_node_t *node, int where) {
    if (where == MXML_WS_AFTER_OPEN || where == MXML_WS_AFTER_CLOSE)
        return ("\n");
    return (NULL);
}

int main(int argc, char *argv[]) {
#ifdef __PS4__
    Notify("%s", __TIME__);
    char *buffer;
    char *buffer2;
    u64 size = 0;
    u64 size2 = 0;
    char *input_file = "/data/GoldHEN/test.xml";
    s32 res = Read_File(input_file, &buffer, &size, 0);

    if (res) {
        Notify("file %s not found\n error: 0x%08x", input_file, res);
        return 0;
    }
#endif

#ifdef __PC__
    char *input_file = argv[1];
    puts(input_file);
    char *buffer = 0;
    u64 length = 0;
    FILE *f = fopen(input_file, "rb");

    if (f) {
        fseek(f, 0, SEEK_END);
        length = ftell(f);
        fseek(f, 0, SEEK_SET);
        buffer = malloc(length);
        if (buffer) {
            fread(buffer, 1, length, f);
        }
        fclose(f);
    }
#endif

    if (buffer) {
        mxml_node_t *node, *tree = NULL;
        tree = mxmlLoadString(NULL, buffer, MXML_NO_CALLBACK);

        if (!tree) {
            printf("XML: could not parse XML:\n%s\n", buffer);
            mxmlDelete(tree);
            free(buffer);
            return 1;
        }

        for (node = mxmlFindElement(tree, tree, "Metadata", NULL, NULL, MXML_DESCEND); node != NULL;
             node = mxmlFindElement(node, tree, "Metadata", NULL, NULL, MXML_DESCEND)) {
            const char *TitleData = GetXMLAttr(node, "Title");
            const char *NameData = GetXMLAttr(node, "Name");
            const char *AuthorData = GetXMLAttr(node, "Author");
            const char *NoteData = GetXMLAttr(node, "Note");
            const char *AppVerData = GetXMLAttr(node, "AppVer");
            const char *AppElfData = GetXMLAttr(node, "AppElf");

            printf("Title: \"%s\" ", TitleData);
            printf("Name: \"%s\" ", NameData);
            printf("Author: \"%s\" ", AuthorData);
            printf("AppVer: \"%s\" ", AppVerData);
            printf("AppElf: \"%s\" ", AppElfData);
            printf("Note: \"%s\"\n", NoteData);

            mxml_node_t *Patchlist_node = mxmlFindElement(node, node, "PatchList", NULL, NULL, MXML_DESCEND);
            char* code = Patchlist_node ? mxmlSaveAllocString(Patchlist_node, &xml_whitespace_cb) : calloc(1, 1);
            puts(code);
            free(code);

            for (mxml_node_t* Line_node = mxmlFindElement(node, node, "Line", NULL, NULL, MXML_DESCEND); Line_node != NULL;
                 Line_node = mxmlFindElement(Line_node, Patchlist_node, "Line", NULL, NULL, MXML_DESCEND)) {
                u64 addr_real = 0;
                const char *gameType = GetXMLAttr(Line_node, "Type");
                const char *gameAddr = GetXMLAttr(Line_node, "Address");
                const char *gameValue = GetXMLAttr(Line_node, "Value");
                printf("Type: \"%s\" ", gameType);
                addr_real = strtoull(gameAddr, NULL, 16);
                printf("Address: \"%s\" (hex 0x%lx) ", gameAddr, addr_real);
                printf("Value: \"%s\"\n", gameValue);
            }
        }
        mxmlDelete(node);
        mxmlDelete(tree);
        free(buffer);
        printf("Build Time: %s\n", __TIME__);
        return 0;
    }
    printf("File %s empty\n", input_file);
    return 1;
}
