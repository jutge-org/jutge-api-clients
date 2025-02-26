import java.io.FileOutputStream;

import com.jutge.api.JutgeApiClient;

class TestException extends Exception {
}

public class Test {

    public static final String ANSI_RESET = "\u001B[0m";
    public static final String ANSI_BLACK = "\u001B[30m";
    public static final String ANSI_RED = "\u001B[31m";
    public static final String ANSI_GREEN = "\u001B[32m";
    public static final String ANSI_YELLOW = "\u001B[33m";
    public static final String ANSI_BLUE = "\u001B[34m";
    public static final String ANSI_PURPLE = "\u001B[35m";
    public static final String ANSI_CYAN = "\u001B[36m";
    public static final String ANSI_WHITE = "\u001B[37m";

    static void check(boolean b) throws TestException {
        if (!b) {
            throw new TestException();
        }
    }

    static void test_tables() throws Exception {
        JutgeApiClient client = new JutgeApiClient();
        JutgeApiClient.AllTables tables = client.tables.get();
        check(tables.languages.size() == 5);
    }

    static void test_logo() throws Exception {
        JutgeApiClient client = new JutgeApiClient();
        JutgeApiClient.Download download = client.misc.getLogo();
        check(download.name.equals("jutge.png"));
        check(download.type.equals("image/png"));
        FileOutputStream fos = new FileOutputStream("logo.png");
        fos.write(download.data);
        fos.close();
    }

    public static void main(String[] args) throws Exception {
        try {
            test_tables();
            test_logo();

            System.out.println(ANSI_GREEN + "All Java tests passed" + ANSI_RESET);
        } catch (TestException error) {
            System.out.println(ANSI_RED + "Java test failed" + ANSI_RESET);
        }
    }
}