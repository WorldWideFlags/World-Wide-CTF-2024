program FreeMyManUAF;

uses crt, SysUtils;

type
  // Define the record (structure) for a request
  Request = record
    Title: String[64];
    Content: String[241];
    callback: procedure;
  end;

  // Define a second structure with no function pointer
  Data = record
    Title: String[64];
    Buffer: String[255];
  end;

  PRequest = ^Request; // Alias for a pointer to Request
  PData = ^Data;       // Alias for a pointer to Data

procedure request_success;
begin
  writeln('There was an error with your string.');
end;

// Procedure to add a request
procedure add_request(req: PRequest);
begin
  writeln('Adding a new request:');
  write('Enter Title: ');
  readln(req^.Title);
  write('Enter Content: ');
  readln(req^.Content);
  req^.callback := @request_success;
  writeln('Request added successfully!');
end;

// Procedure to edit a request
procedure edit_request(req: PRequest);
begin
  writeln('Editing the request:');
  write('New Title: ');
  readln(req^.Title);
  write('New Content: ');
  readln(req^.Content);
  writeln('Request updated successfully!');
end;

// Procedure to delete a request
procedure delete_request(req: PRequest);
begin
  writeln('Deleting the request.');
  FreeMem(req);
  writeln('Request deleted successfully!');
end;

// Procedure to show a request
procedure show_request(req: PRequest);
begin
  writeln('Request Details:');
  if req^.Title = '' then
    req^.callback()
  else
  begin
    writeln('Title: ', req^.Title);
    writeln('Content: ', req^.Content);
  end;
end;

// Procedure to add a data structure
procedure add_data(dat: PData);
begin
  writeln('Adding data:');
  write('Enter Title: ');
  readln(dat^.Title);
  write('Enter Buffer Content: ');
  readln(dat^.Buffer);
  writeln('Data added successfully!');
end;

var
  choice, req_number, data_number: Integer;
  reqs: array[1..10] of PRequest; // Array of pointers to requests
  datas: array[1..10] of PData;   // Array of pointers to data
  count_req, count_data: Integer;

begin
  clrscr;
  count_req := 0;
  count_data := 0;
  writeln('Free My Man Pascal');
  writeln('==================================');
  repeat
    writeln('1. Add a request');
    writeln('2. Edit a request');
    writeln('3. Show a request');
    writeln('4. Delete a request');
    writeln('5. Add data');
    writeln('6. Exit');
    write('>> ');
    readln(choice);

    case choice of
      1: begin
           if count_req >= 10 then
           begin
             writeln('You have too many requests already.');
           end
           else
           begin
             inc(count_req);
             GetMem(reqs[count_req], SizeOf(Request)); // Allocate memory for a new request
             add_request(reqs[count_req]);
           end;
         end;

      2: begin
           if count_req = 0 then
           begin
             writeln('No requests to edit.');
           end
           else
           begin
             write('Enter request number to edit (1-', count_req, '): ');
             readln(req_number);
             if (req_number >= 1) and (req_number <= count_req) then
               edit_request(reqs[req_number])
             else
             begin
               writeln('Invalid request number.');
             end;
           end;
         end;

      3: begin
           if count_req = 0 then
           begin
             writeln('No requests to show.');
           end
           else
           begin
             write('Enter request number to show: ');
             readln(req_number);
             if (req_number >= 1) and (req_number <= count_req) then
                show_request(reqs[req_number])
             else
             begin
               writeln('Invalid request number.');
             end;
           end;
         end;

      4: begin
           if count_req = 0 then
           begin
             writeln('No requests to delete.');
           end
           else
           begin
             Flush(Output);

             writeln('Enter request number to delete: ');
             readln(req_number);
             if (req_number >= 1) and (req_number <= count_req) then
             begin
               delete_request(reqs[req_number]);
             end
             else
             begin
               writeln('Invalid request number.');
             end;
           end;
         end;

      5: begin
           if count_data >= 10 then
           begin
             writeln('You have too much data already.');
           end
           else
           begin
             inc(count_data);
             GetMem(datas[count_data], SizeOf(Data)); // Allocate memory for new data
             add_data(datas[count_data]);
           end;
         end;

      6: begin
           writeln('Exiting program...');
         end;

    else
      writeln('Invalid choice. Please try again.');
    end;

  until choice = 6;
end.
