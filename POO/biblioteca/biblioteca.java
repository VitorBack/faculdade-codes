import java.util.ArrayList;

public class biblioteca {
    ArrayList<livro> acervoLivros;
    ArrayList<cliente> cadastroClientes;
    ArrayList<emprestimo> historicoEmprestimos;

    public biblioteca() {
        this.acervoLivros = new ArrayList<>();
        this.cadastroClientes = new ArrayList<>();
        this.historicoEmprestimos = new ArrayList<>();
    }

    public void adicionarLivro(livro livro) {
        acervoLivros.add(livro);
    }

    public void cadastrarCliente(cliente cliente) {
        cadastroClientes.add(cliente);
    }

    public void emprestarLivro(livro livro, cliente cliente, String dataEmprestimo, String dataDevolucaoPrevista) {
        if (livro.isDisponivel()) {
            emprestimo novoEmprestimo = new emprestimo(livro, cliente, dataEmprestimo, dataDevolucaoPrevista);
            historicoEmprestimos.add(novoEmprestimo);
            livro.setDisponivel(false);
            System.out.println("Empréstimo realizado com sucesso!");
        } else {
            System.out.println("Desculpe, o livro '" + livro.getTitulo() + "' não está disponível no momento.");
        }
    }

    public livro buscarLivroPorTitulo(String titulo) {
        for (livro livro : acervoLivros) {
            if (livro.getTitulo().equals(titulo)) {
                return livro;
            }
        }
        return null;
    }

    public cliente buscarClientePorNome(String nome) {
        for (cliente cliente : cadastroClientes) {
            if (cliente.getNome().equals(nome)) {
                return cliente;
            }
        }
        return null;
    }

    public void buscarLivroPorTituloExibir(String titulo) {
        livro livroEncontrado = buscarLivroPorTitulo(titulo);
        if (livroEncontrado != null) {
            livroEncontrado.exibirInformacoes();
        } else {
            System.out.println("Livro com título '" + titulo + "' não encontrado.");
        }
    }

    public void buscarClientePorNomeExibir(String nome) {
        cliente clienteEncontrado = buscarClientePorNome(nome);
        if (clienteEncontrado != null) {
            clienteEncontrado.exibirInformacoes();
        } else {
            System.out.println("Cliente com nome '" + nome + "' não encontrado.");
        }
    }

    public void listarLivrosDisponiveis() {
        System.out.println("Livros disponíveis:");
        boolean encontrado = false;
        for (livro livro : acervoLivros) {
            if (livro.isDisponivel()) {
                encontrado = true;
                livro.exibirInformacoes();
                System.out.println("--------------------");
            }
        }
        if (!encontrado) {
            System.out.println("Nenhum livro disponível no momento.");
        }
    }

    public void listarEmprestimosAtivos() {
        System.out.println("Empréstimos ativos:");
        boolean encontrado = false;
        for (emprestimo emprestimo : historicoEmprestimos) {
            if (emprestimo.getDataDevolucaoRealizada() == null) {
                encontrado = true;
                emprestimo.exibirInformacoes();
                System.out.println("--------------------");
            }
        }
        if (!encontrado) {
            System.out.println("Nenhum empréstimo ativo no momento.");
        }
    }

    public void devolverLivro(String isbn, String dataDevolucaoRealizada) {
        for (emprestimo emprestimo : historicoEmprestimos) {
            if (emprestimo.getLivro().getIsbn().equals(isbn) && emprestimo.getDataDevolucaoRealizada() == null) {
                emprestimo.setDataDevolucaoRealizada(dataDevolucaoRealizada);
                emprestimo.getLivro().setDisponivel(true);
                System.out.println("Devolução realizada com sucesso!");
                return;
            }
        }
        System.out.println("Nenhum empréstimo ativo encontrado para o ISBN '" + isbn + "'.");
    }
}
