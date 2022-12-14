#include "tiny-json/tiny-json.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAX_TOKENS 10240 // should be plenty
#define debug_printf(a, args...) printf("[%s] (%s:%d) " a, __func__, __FILE__, __LINE__, ##args)

#define KEY_PATCH "patch"
#define KEY_TITLE "title"
#define KEY_APP_VER "app_ver"
#define KEY_PATCH_VER "patch_ver"
#define KEY_NAME "name"
#define KEY_AUTHOR "author"
#define KEY_NOTE "note"
#define KEY_APP_TITLEID "app_titleid"
#define KEY_APP_ELF "app_elf"
#define KEY_APP_TYPE "type"
#define KEY_APP_ADDR "addr"
#define KEY_APP_VALUE "value"
#define KEY_PATCH_LIST "patch_list"
#define KEY_COMMENT "comment"

int main(int argc, char *argv[]) {
    if (argc == 2) {
        char *str = 0;
        uint64_t length = 0;
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

        json_t mem[MAX_TOKENS];
        json_t const *json = json_create(str, mem, MAX_TOKENS);
        if (!json) {
            printf("Error json create\n");
            return 1;
        }

        debug_printf("read: %s size: %lu bytes\n", argv[1], length);
        json_t const *patchItems = json_getProperty(json, KEY_PATCH);
        if (!patchItems || JSON_ARRAY != json_getType(patchItems)) {
            printf("Error, the %s list property is not found\n", KEY_PATCH);
            return 1;
        }

        json_t const *patches;
        for (patches = json_getChild(patchItems); patches != 0;
             patches = json_getSibling(patches)) {
            if (JSON_OBJ == json_getType(patches)) {
                char const *gameTitle = json_getPropertyValue(patches, KEY_TITLE);
                if (gameTitle)
                    debug_printf("%s: %s\n", KEY_TITLE, gameTitle);
                else
                    debug_printf("%s: not found\n", KEY_TITLE);
                char const *gameAppver = json_getPropertyValue(patches, KEY_APP_VER);
                if (gameAppver)
                    debug_printf("%s: %s\n", KEY_APP_VER, gameAppver);
                else
                    debug_printf("%s: not found\n", KEY_APP_VER);
                char const *gameName = json_getPropertyValue(patches, KEY_NAME);
                if (gameName)
                    debug_printf("%s: %s\n", KEY_NAME, gameName);
                else
                    debug_printf("%s: not found\n", KEY_NAME);
                char const *gameAuthor = json_getPropertyValue(patches, KEY_AUTHOR);
                if (gameAuthor)
                    debug_printf("%s: %s\n", KEY_AUTHOR, gameAuthor);
                else
                    debug_printf("%s: not found\n", KEY_AUTHOR);
                char const *gameNote = json_getPropertyValue(patches, KEY_NOTE);
                if (gameNote)
                    debug_printf("%s: %s\n", KEY_NOTE, gameNote);
                else
                    debug_printf("%s: not found\n", KEY_NOTE);
                json_t const *patch_List_Items = json_getProperty(patches, KEY_PATCH_LIST);
                json_t const *patch_lists;
                for (patch_lists = json_getChild(patch_List_Items); patch_lists != 0;
                     patch_lists = json_getSibling(patch_lists)) {
                    if (JSON_OBJ == json_getType(patch_lists)) {
                        char const *gameType = json_getPropertyValue(patch_lists, KEY_APP_TYPE);
                        if (gameType)
                            debug_printf("  %s: %s\n", KEY_APP_TYPE, gameType);
                        char const *gameAddr = json_getPropertyValue(patch_lists, KEY_APP_ADDR);
                        if (gameAddr)
                            debug_printf("  %s: %s\n", KEY_APP_ADDR, gameAddr);
                        char const *gameValue = json_getPropertyValue(patch_lists, KEY_APP_VALUE);
                        if (gameValue)
                            debug_printf("  %s: %s\n", KEY_APP_VALUE, gameValue);
                        char const *gameComm = json_getPropertyValue(patch_lists, KEY_COMMENT);
                        if (gameComm)
                            debug_printf("  %s: %s\n", KEY_COMMENT, gameComm);
                    }
                }
            }
        }
        free(str);
        debug_printf("free: %lu bytes from memory\n", length);
        printf("json_create(%s); // check passed\n", argv[1]);
        return 0;
    }
    printf("no file provided\n");
    return 1;
}
