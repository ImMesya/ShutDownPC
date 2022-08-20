#include "ShutDownPC.h"
#include <QtWidgets/QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    ShutDownPC w;
    w.show();
    return a.exec();
}
