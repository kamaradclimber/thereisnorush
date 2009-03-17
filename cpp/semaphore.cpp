void Semaphore::open()
{
    if (red || yellow || !green)
    {
        red = yellow = false;
        green = true;

        touch();
    }
}

void Semaphore::touch()
{
    last_update = clock();
}
