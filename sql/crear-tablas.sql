create table if not exists frecuency_dictionary (
  density_text TEXT  NOT NULL
);

insert into frecuency_dictionary (density_text) VALUES ('        aaaaaabccdddeeeeeeefghiiijkllmmnnnooooppqrrrssssttuuvwxyz!@#$%^&*().,
        AAAAAABCCDDDEEEEEEEFGHIIIJKLLMMNNNOOOOPPQRRRSSSSTTUUVWXYZ');

create table if not exists encoding_info (
  id SERIAL PRIMARY KEY,
  encode_text TEXT NOT NULL, 
  decode_text TEXT NOT NULL
);