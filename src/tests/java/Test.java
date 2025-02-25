import java.io.FileOutputStream;
import java.lang.reflect.Method;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

class TestException extends Exception {
}

/*
 * Uses reflection to find all public methods that start with Test
 * and executes them checking their assertions written with check.
 */

public class Test {

    public static boolean ok = true;

    public static final String ANSI_RESET = "\u001B[0m";
    public static final String ANSI_BLACK = "\u001B[30m";
    public static final String ANSI_RED = "\u001B[31m";
    public static final String ANSI_GREEN = "\u001B[32m";
    public static final String ANSI_YELLOW = "\u001B[33m";
    public static final String ANSI_BLUE = "\u001B[34m";
    public static final String ANSI_PURPLE = "\u001B[35m";
    public static final String ANSI_CYAN = "\u001B[36m";
    public static final String ANSI_WHITE = "\u001B[37m";

    public static void check(boolean b) throws TestException {
        if (!b) {
            throw new TestException();
        }
    }

    public static void test(String name) throws Exception {
        Class<Test> klass = Test.class;
        Method method = klass.getMethod(name);
        Object[] parameters = new Object[0];
        try {
            method.invoke(null, parameters);
            System.out.println(ANSI_GREEN + name + ANSI_RESET);
        } catch (Exception error) {
            ok = false;
            System.out.println(ANSI_RED + name + ANSI_RESET);
        }
    }

    public static void TestTables() throws Exception {
        JutgeApiClient jutge = new JutgeApiClient();
        JutgeApiClient.AllTables tables = jutge.tables.get();
        check(tables.languages.size() == 5); // hard coded
    }

    public static void TestLogo() throws Exception {
        JutgeApiClient jutge = new JutgeApiClient();
        JutgeApiClient.Download download = jutge.misc.getLogo();
        check(download.name.equals("jutge.png"));
        check(download.type.equals("image/png"));
        FileOutputStream fos = new FileOutputStream("logo.png");
        fos.write(download.data);
        fos.close();
        Path path = Paths.get("logo.png");
        long size = Files.size(path);
        check(size == 52950); // hard coded value
    }

    public static void TestProblem() throws Exception {
        JutgeApiClient jutge = new JutgeApiClient();
        var problem = jutge.problems.getProblem("P68688_en");
        check(problem.title.equals("Hello world!"));
        check(problem.abstract_problem.author.equals("Jordi Petit"));
    }

    public static void main(String[] args) throws Exception {
        Method[] allMethods = Test.class.getDeclaredMethods();
        for (Method method : allMethods) {
            if (method.getName().startsWith("Test")) {
                test(method.getName());
            }
        }
        if (ok) {
            System.out.println(ANSI_GREEN + "All Java tests passed" + ANSI_RESET);
        } else {
            System.out.println(ANSI_RED + "Some Java test failed" + ANSI_RESET);
        }
    }

}