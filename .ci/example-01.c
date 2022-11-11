#include "tiny-json/tiny-json.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_TOKENS 4096
#define debug_printf(a, args...) printf("[%s] (%s:%d) " a, __func__, __FILE__, __LINE__, ##args)

int main(int argc, char *argv[]) {
    if (argc == 2) {
        char *str = 0;
        long length;
        FILE *f = fopen(argv[1], "r");
        if (f) {
            fseek(f, 0, SEEK_END);
            length = ftell(f);
            fseek(f, 0, SEEK_SET);
            str = malloc(length);
            if (str) {
                fread(str, 1, length, f);
            }
            fclose(f);
        }
        json_t mem[MAX_TOKENS]; // should be plenty
        json_t const *json = json_create(str, mem, sizeof mem / sizeof *mem);
        if (!json) {
            printf("Error json create\n");
            return 1;
        }

        json_t const *patchItems = json_getProperty(json, "patch");
        if (!patchItems || JSON_ARRAY != json_getType(patchItems)) {
            printf("Error, the patches list property is not found\n");
            return 1;
        }

        json_t const *patches;
        for (patches = json_getChild(patchItems); patches != 0;
             patches = json_getSibling(patches)) {
            if (JSON_OBJ == json_getType(patches)) {
                char const *gameTitle = json_getPropertyValue(patches, "title");
                if (gameTitle)
                    debug_printf("title: %s\n", gameTitle);
                char const *gameAppver = json_getPropertyValue(patches, "app_ver");
                if (gameAppver)
                    debug_printf("app_ver: %s\n", gameAppver);
                char const *gameName = json_getPropertyValue(patches, "name");
                if (gameName)
                    debug_printf("name: %s\n", gameName);
                char const *gameAuthor = json_getPropertyValue(patches, "author");
                if (gameAuthor)
                    debug_printf("author: %s\n", gameAuthor);
                char const *gameNote = json_getPropertyValue(patches, "note");
                if (gameNote)
                    debug_printf("note: %s\n", gameNote);
                json_t const *patch_List_Items = json_getProperty(patches, "patch_list");
                json_t const *patch_lists;
                for (patch_lists = json_getChild(patch_List_Items); patch_lists != 0;
                     patch_lists = json_getSibling(patch_lists)) {
                    if (JSON_OBJ == json_getType(patch_lists)) {
                        char const *gameType = json_getPropertyValue(patch_lists, "type");
                        if (gameType)
                            debug_printf("  type: %s\n", gameType);
                        char const *gameAddr = json_getPropertyValue(patch_lists, "address");
                        if (gameAddr)
                            debug_printf("  addr: %s\n", gameAddr);
                        char const *gameValue = json_getPropertyValue(patch_lists, "value");
                        if (gameValue)
                            debug_printf("  val: %s\n", gameValue);
                    }
                }
            }
        }
        printf("json_create( str = %s); // check passed\n", argv[1]);
        return 0;
    }
    printf("no file provided\n");
    return 1;
}
