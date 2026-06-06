package com.example.aicicd;

import org.junit.Test;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertThrows;

public class CalculatorTest {
    private final Calculator calculator = new Calculator();

    @Test
    public void addReturnsSum() {
        assertEquals(5, calculator.add(2, 3));
    }

    @Test
    public void subtractReturnsDifference() {
        assertEquals(4, calculator.subtract(9, 5));
    }

    @Test
    public void multiplyReturnsProduct() {
        assertEquals(42, calculator.multiply(6, 7));
    }

    @Test
    public void divideReturnsQuotient() {
        assertEquals(3, calculator.divide(9, 3));
    }

    @Test
    public void divideRejectsZeroDivisor() {
        IllegalArgumentException error = assertThrows(
                IllegalArgumentException.class,
                () -> calculator.divide(9, 0)
        );

        assertEquals("Division by zero is not allowed.", error.getMessage());
    }
}
