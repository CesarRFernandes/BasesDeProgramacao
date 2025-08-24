package serializar;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.ObjectOutputStream;

public class Principal {
    public static void main(String[] args) {
        Professor p1 = new Professor("Miguel",42,"2345");
        try {
        FileOutputStream arqSer = new FileOutputStream("c:/arquivo/miguel.ser");
        ObjectOutputStream oSer = new ObjectOutputStream(arqSer);
        oSer.writeObject(p1);
        oSer.close();
        arqSer.close();

        p1.setTelefone("21");

        System.out.println(p1);
        System.out.println(".......................");
        FielInputStream arqDes = new FileInputStream();
        } catch (FileNotFoundException e){
            e.printStackTrace();
        }
    }
}
