package serializar;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
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
        FielInputStream arqDes = new FileInputStream("c:/arquivo/miguel.ser");
        ObjectInputStream oDes = new ObjectInputStream("arqDes");
        p1 = (Pessoa) oDes.readObject();
        oDes.close();
        arqDes.close();
        System.out.println("........................");
        System.out.println(p1);
        } catch (FileNotFoundException e){
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (ClassNotFoundException e){
            e.printStackTrace();
        }
    }
}
