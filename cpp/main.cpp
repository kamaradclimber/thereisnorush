#include <iostream>
#include "main.hpp" 

using namespace std;

int main(int argc, char **argv) {    
    float time_last_counter = 0.;

    QApplication application(argc, argv);
    
    //Map map;
    //map.load_demo_map();
        
    MainWindow main_window;
    main_window.showMaximized();

    /*while (true) {
        main_window.update();
    }*/

    return application.exec();
}

