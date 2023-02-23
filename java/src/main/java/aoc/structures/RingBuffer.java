package aoc.structures;

import java.util.LinkedList;
import java.util.List;
import java.util.stream.Stream;

public class RingBuffer<T> {
    private LinkedList<T> items;
    private int pointer;

    public RingBuffer(Stream<T> stream) {
        this.pointer = 0;
        this.items = new LinkedList<>();
        this.items.addAll(stream.toList());
    }

    public void rotate(int offset) {
        this.pointer += offset;
        if (this.pointer < 0) {
            int sizeMultiple = this.items.size() * (((this.pointer * -1) / this.items.size()) + 1);
            this.pointer += sizeMultiple;
        }
        this.pointer = this.pointer % this.items.size();
    }

    public T peek() {
        return this.items.get(this.pointer);
    }

    public T removeLeft() {
        T value = this.items.remove(this.pointer);
        if (this.pointer > this.items.size()) {
            this.pointer = 0;
        }
        return value;
    }

    public void appendLeft(T value) {
        this.items.add(this.pointer, value);
        this.pointer += 1;
    }

    public List<T> toList() {
        this.rotate(-this.pointer);
        return this.items.stream().toList();
    }
}
