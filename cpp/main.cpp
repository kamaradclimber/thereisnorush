#include "main.hpp" 

using namespace std;

int main(int argc, char **argv)
{    
    unsigned float time_last_counter = 0.0;

    QApplication application(argc, argv);
    
    
    Map map;
        map.load_demo_map();
        
    MainWindow main_window;
        main_window.showMaximized();

    return application.exec();
}

