interface Iterator<T> {
    boolean hasNext();
    T next();
}

class ArrayIterator<T> implements Iterator<T> {
    private T[] items;
    private int position;

    public ArrayIterator(T[] items) {
        this.items = items;
        this.position = 0;
    }

    @Override
    public boolean hasNext() {
        return position < items.length;
    }

    @Override
    public T next() {
        if (this.hasNext()) {
            return items[position++];
        }
        throw new ArrayIndexOutOfBoundsException();
    }
}