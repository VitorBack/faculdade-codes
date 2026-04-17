import java.util.Scanner;

public class SistemaBiblioteca {
    public static void main(String[] args) {
        biblioteca minhaBiblioteca = new biblioteca();
        Scanner scanner = new Scanner(System.in);// pra ler o que o usuario digitar

        minhaBiblioteca.adicionarLivro(new livro("O Senhor dos Anéis", "J.R.R. Tolkien", "1234567890", 1954));
        minhaBiblioteca
                .adicionarLivro(new livro("Harry Potter e a Pedra Filosofal", "J.K. Rowling", "0987654321", 1997));
        minhaBiblioteca.cadastrarCliente(new cliente("João Silva", "123.456.789-00", "Rua A, 123", "(11) 98765-4321"));

        boolean continuar = true;
        while (continuar) {
            exibirMenu();
            System.out.print("Escolha uma opção: ");
            String opcao = scanner.nextLine().trim();// .trim() tira os espaços em branco

            switch (opcao) { // Menu de opções
                case "1":
                    cadastrarLivro(minhaBiblioteca, scanner);
                    break;
                case "2":
                    cadastrarCliente(minhaBiblioteca, scanner);
                    break;
                case "3":
                    realizarEmprestimo(minhaBiblioteca, scanner);
                    break;
                case "4":
                    realizarDevolucao(minhaBiblioteca, scanner);
                    break;
                case "5":
                    buscarLivroPorTitulo(minhaBiblioteca, scanner);
                    break;
                case "6":
                    buscarClientePorNome(minhaBiblioteca, scanner);
                    break;
                case "7":
                    minhaBiblioteca.listarLivrosDisponiveis();
                    break;
                case "8":
                    minhaBiblioteca.listarEmprestimosAtivos();
                    break;
                case "0":
                    continuar = false;
                    System.out.println("Encerrando o sistema. Obrigado!");
                    break;
                default:
                    System.out.println("Opção inválida. Tente novamente.");
                    break;
            }

            System.out.println();
        }

        scanner.close();
    }

    private static void exibirMenu() {
        System.out.println("=== Sistema de Biblioteca ===");
        System.out.println("1 - Cadastrar novo livro");
        System.out.println("2 - Cadastrar novo cliente");
        System.out.println("3 - Realizar empréstimo");
        System.out.println("4 - Realizar devolução");
        System.out.println("5 - Buscar livro por título");
        System.out.println("6 - Buscar cliente por nome");
        System.out.println("7 - Listar livros disponíveis");
        System.out.println("8 - Listar empréstimos ativos");
        System.out.println("0 - Sair");
    }

    private static void cadastrarLivro(biblioteca biblioteca, Scanner scanner) {
        System.out.print("Título: ");
        String titulo = scanner.nextLine().trim();
        System.out.print("Autor: ");
        String autor = scanner.nextLine().trim();
        System.out.print("ISBN: ");
        String isbn = scanner.nextLine().trim();
        System.out.print("Ano de publicação: ");
        int anoPublicacao = Integer.parseInt(scanner.nextLine().trim()); // Converte a entrada para um número inteiro

        biblioteca.adicionarLivro(new livro(titulo, autor, isbn, anoPublicacao));
        System.out.println("Livro cadastrado com sucesso!");
    }

    private static void cadastrarCliente(biblioteca biblioteca, Scanner scanner) {
        System.out.print("Nome: ");
        String nome = scanner.nextLine().trim();
        System.out.print("CPF: ");
        String cpf = scanner.nextLine().trim();
        System.out.print("Endereço: ");
        String endereco = scanner.nextLine().trim();
        System.out.print("Telefone: ");
        String telefone = scanner.nextLine().trim();

        biblioteca.cadastrarCliente(new cliente(nome, cpf, endereco, telefone));
        System.out.println("Cliente cadastrado com sucesso!");
    }

    private static void realizarEmprestimo(biblioteca biblioteca, Scanner scanner) {
        System.out.print("Título do livro: ");
        String titulo = scanner.nextLine().trim();
        System.out.print("Nome do cliente: ");
        String nomeCliente = scanner.nextLine().trim();

        livro livro = biblioteca.buscarLivroPorTitulo(titulo);
        cliente cliente = biblioteca.buscarClientePorNome(nomeCliente);

        if (livro == null) {
            System.out.println("Livro não encontrado.");
            return;
        }
        if (cliente == null) {
            System.out.println("Cliente não encontrado.");
            return;
        }

        System.out.print("Data de empréstimo (dd/MM/yyyy): ");
        String dataEmprestimo = scanner.nextLine().trim();
        System.out.print("Data de devolução prevista (dd/MM/yyyy): ");
        String dataDevolucaoPrevista = scanner.nextLine().trim();

        biblioteca.emprestarLivro(livro, cliente, dataEmprestimo, dataDevolucaoPrevista);
    }

    private static void realizarDevolucao(biblioteca biblioteca, Scanner scanner) {
        System.out.print("ISBN do livro: ");
        String isbn = scanner.nextLine().trim();
        System.out.print("Data de devolução realizada (dd/MM/yyyy): ");
        String dataDevolucaoRealizada = scanner.nextLine().trim();

        biblioteca.devolverLivro(isbn, dataDevolucaoRealizada);
    }

    private static void buscarLivroPorTitulo(biblioteca biblioteca, Scanner scanner) {
        System.out.print("Título do livro: ");
        String titulo = scanner.nextLine().trim();
        biblioteca.buscarLivroPorTituloExibir(titulo);
    }

    private static void buscarClientePorNome(biblioteca biblioteca, Scanner scanner) {
        System.out.print("Nome do cliente: ");
        String nome = scanner.nextLine().trim();
        biblioteca.buscarClientePorNomeExibir(nome);
    }
}
