import java.io.FileOutputStream;

public class Test {
    public static void main(String[] args) throws Exception {
        JutgeApiClient client = new JutgeApiClient();

        JutgeApiClient.AllTables tables = client.tables.get();
        System.out.println(tables.languages.size());

        var languages = client.tables.getLanguages();
        for (JutgeApiClient.Language l : languages.values()) {
            System.out.println(l.language_id + " " + l.eng_name);
        }

        JutgeApiClient.Download download = client.misc.getLogo();
        System.out.println(download.name);
        System.out.println(download.type);

        FileOutputStream fos = new FileOutputStream("logo.png");
        fos.write(download.data);
        fos.close();

        client.auth.logout();
        client.meta = null;
    }
}