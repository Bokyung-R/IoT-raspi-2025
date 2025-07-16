#include <stdio.h>
#include <string.h>
#include <memory.h>

int main()
{
    FILE *fp;
    int type = 0;

    printf("(회원가입 : 0 / 로그인 : 1) 입력 후 엔터 : ");
    scanf("%d", &type);
    getchar();

    if (type == 0)
    {
        fp = fopen("userFile.txt", "a+");
        if (fp == NULL) {
            printf("파일 열기 실패\n");
            return 1;
        }

        char ID[20], PW[20], value[50], file_buff[50];
        memset(ID, 0, sizeof(ID));
        memset(PW, 0, sizeof(PW));
        memset(value, 0, sizeof(value));
        memset(file_buff, 0, sizeof(file_buff));

        printf("회원가입입니다.\n");
        printf("아이디를 입력해주세요 : ");
        scanf("%s", ID);
        printf("비밀번호를 입력해주세요 : ");
        scanf("%s", PW);

        sprintf(value, "%s %s\n", ID, PW);

        rewind(fp);
        while (fgets(file_buff, sizeof(file_buff), fp) != NULL) {
            if (strcmp(file_buff, value) == 0) {
                printf("동일한 ID, PW가 존재합니다\n");
                fclose(fp);
                return 0;
            }
        }

        fputs(value, fp);
        printf("회원가입이 완료되었습니다.\n");
        fclose(fp);
    }
    else if (type == 1)
    {
        fp = fopen("userFile.txt", "r");
        if (fp == NULL) {
            printf("파일 열기 실패\n");
            return 1;
        }

        char ID[20], PW[20], value[50], file_buff[50];
        memset(ID, 0, sizeof(ID));
        memset(PW, 0, sizeof(PW));
        memset(value, 0, sizeof(value));
        memset(file_buff, 0, sizeof(file_buff));

        printf("로그인입니다\n");
        printf("아이디를 입력해주세요 : ");
        scanf("%s", ID);
        printf("비밀번호를 입력해주세요 : ");
        scanf("%s", PW);

        sprintf(value, "%s %s", ID, PW);

        while (fgets(file_buff, sizeof(file_buff), fp) != NULL) {
            file_buff[strcspn(file_buff, "\n")] = '\0';

            if (strcmp(file_buff, value) == 0) {
                printf("로그인되었습니다.\n");
                fclose(fp);
                return 0;
            }
        }

        printf("아이디나 비밀번호가 틀렸습니다\n");
        fclose(fp);
    }
    else {
        printf("0 또는 1만 입력해주세요\n");
    }

    return 0;
}
