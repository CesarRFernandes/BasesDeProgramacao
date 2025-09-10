package main.java.com.poa4.ap6;
import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/processar-curriculo")
public class CurriculoServlet extends HttpServlet {
    private static final long serialVersionUID = 1L;

    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        request.setCharacterEncoding("UTF-8");
        response.setCharacterEncoding("UTF-8");

        String nome = request.getParameter("nome");
        String idade = request.getParameter("idade");
        String escolaridade = request.getParameter("escolaridade");
        String[] areasInteresse = request.getParameterValues("areaInteresse");
        String experiencia = request.getParameter("experiencia");

        if (nome == null || nome.trim().isEmpty()) {
            request.setAttribute("erro", "Nome é obrigatório");
            request.getRequestDispatcher("cadastro-curriculo.jsp").forward(request, response);
            return;
        }

        if (idade == null || idade.trim().isEmpty()) {
            request.setAttribute("erro", "Idade é obrigatória");
            request.getRequestDispatcher("cadastro-curriculo.jsp").forward(request, response);
            return;
        }

        StringBuilder areasFormatadas = new StringBuilder();
        if (areasInteresse != null && areasInteresse.length > 0) {
            for (int i = 0; i < areasInteresse.length; i++) {
                areasFormatadas.append(areasInteresse[i]);
                if (i < areasInteresse.length - 1) {
                    areasFormatadas.append(", ");
                }
            }
        } else {
            areasFormatadas.append("Não informado");
        }

        if (experiencia == null || experiencia.trim().isEmpty()) {
            experiencia = "Não informado";
        }

        request.setAttribute("nome", nome.trim());
        request.setAttribute("idade", idade.trim());
        request.setAttribute("escolaridade", escolaridade);
        request.setAttribute("areasInteresse", areasFormatadas.toString());
        request.setAttribute("experiencia", experiencia.trim());

        request.getRequestDispatcher("exibir-curriculo.jsp").forward(request, response);
    }

    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.sendRedirect("cadastro-curriculo.jsp");
    }
}