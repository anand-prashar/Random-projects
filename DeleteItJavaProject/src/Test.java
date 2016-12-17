import java.util.Scanner;

public class Test {

	public static void main(String[] args) 
	{
		
		Scanner scan = new Scanner(System.in);
		boolean t = true;
		while(t)
		{
		System.out.println("---------------------------------------\n\n(Yes) :");
		float countYes = scan.nextFloat();
		System.out.println("(No) :");
		float countNo = scan.nextFloat();
		
		float sum = countYes+countNo;
		float total_records = 14;
		
		double entropy = ( (Math.log10(sum/countYes)/Math.log10(2)) * (countYes/sum)) + 
						( (Math.log10(sum/countNo)/Math.log10(2)) * (countNo/sum));
		double result = entropy * sum / total_records;
		
		System.out.println("result = "+result);
		}
		scan.close();
	}

}
