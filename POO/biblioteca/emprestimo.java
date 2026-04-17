public class emprestimo {
    livro livro;
    cliente cliente;
    String dataEmprestimo;
    String dataDevolucaoPrevista;
    String dataDevolucaoRealizada;

    public emprestimo(livro livro, cliente cliente, String dataEmprestimo, String dataDevolucaoPrevista) {
        this.livro = livro;
        this.cliente = cliente;
        this.dataEmprestimo = dataEmprestimo;
        this.dataDevolucaoPrevista = dataDevolucaoPrevista;
        this.dataDevolucaoRealizada = null;
    }

    public livro getLivro() {
        return livro;
    }

    public cliente getCliente() {
        return cliente;
    }

    public String getDataEmprestimo() {
        return dataEmprestimo;
    }

    public String getDataDevolucaoPrevista() {
        return dataDevolucaoPrevista;
    }

    public String getDataDevolucaoRealizada() {
        return dataDevolucaoRealizada;
    }

    public void setDataEmprestimo(String dataEmprestimo) {
        this.dataEmprestimo = dataEmprestimo;
    }

    public void setDataDevolucaoPrevista(String dataDevolucaoPrevista) {
        this.dataDevolucaoPrevista = dataDevolucaoPrevista;
    }

    public void setDataDevolucaoRealizada(String dataDevolucaoRealizada) {
        this.dataDevolucaoRealizada = dataDevolucaoRealizada;
    }

    public void exibirInformacoes() {
        System.out.println("Livro: " + livro.getTitulo());
        System.out.println("Cliente: " + cliente.nome);
        System.out.println("Data de Empréstimo: " + dataEmprestimo);
        System.out.println("Data de Devolução Prevista: " + dataDevolucaoPrevista);
        System.out.println("Data de Devolução Realizada: "
                + (dataDevolucaoRealizada != null ? dataDevolucaoRealizada : "Ainda não devolvido"));
    }
}
