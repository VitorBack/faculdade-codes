public class NumberDisplay {
    private int limit;
    private int value;

    public NumberDisplay(int rollOverLimit){
        limit = rollOverLimit;
        value = 0;
    }

    public NumberDisplay(int rollOverLimit, int v){
        limit = rollOverLimit;
        value = v;
    }

    public void increment(){
        value = (value + 1) % limit;
    }

    public int getValue(){
        return value;
    }

    public String getDisplayValue(){
        if (value<10){
            return "0"+value; 
        }else {
            return ""+value;
        }
    }
}


