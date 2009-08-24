#include "semaphore.hpp"

using namespace std;

Semaphore::Semaphore() : m_state(GREEN) {}


SemaphoreState Semaphore::state() const {
    return m_state;
}

clock_t Semaphore::last_update() const {
    return m_last_update;
}

void Semaphore::set(SemaphoreState new_state) {
    m_state = new_state;
}

void Semaphore::open() {
    /*if (red || yellow || !green) {
        red = yellow = false;
        green = true;

        touch();
    }*/

    m_state = GREEN;
    touch();
}

void Semaphore::touch() {
    m_last_update = clock();
}
