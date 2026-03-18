public class Livro {
    private String titulo;
    private String autor;
    private String isbn;
    private boolean available;

    public Livro(String t, String a, String i){
        titulo = t;
        autor = a;
        isbn = i;
        available = true;
    }

    public String getTitulo(){
        return titulo;
    }

    public String getAutor(){
        return autor;
    }

    public String getIsbn(){
        return isbn;
    }

    public boolean getAvailable(){
        return available;
    }

    public void setAvailable(boolean d){
        available = d;
    }

    public boolean emprestar(){
        if (available == true){
            available = false;
            return true;
        }else {
            return false;
        }
    }

    public void devolver(){
        available = true;
    }

    public void exibirInformacoes(){
        System.out.println("Título do Livro: "+titulo);
        System.out.println("Autor do Livro"+autor);
        System.out.println("ISBN do Livro: "+isbn);
        System.out.println("Disponibilidade: " + (available ? "Sim" : "Não"));
    }
}